'use client';

import React, { useState, useEffect } from 'react';
import { Check, MoveRight, PhoneCall, MessageCircle, Mail, ExternalLink } from "lucide-react";
import { Badge } from "@/components/ui/badge";
import { Card, CardContent, CardDescription, CardHeader, CardTitle } from "@/components/ui/card";
import { Button } from "@/components/ui/button";
import ServiceBookingModal from './ServiceBookingModal';

interface TradingService {
  id: number;
  name: string;
  slug: string;
  service_type: string;
  description: string;
  detailed_description: string;
  price: number;
  currency: string;
  duration: string;
  price_display: string;
  features: string[];
  is_active: boolean;
  is_featured: boolean;
  is_popular: boolean;
  booking_type: string;
  contact_info: string;
  booking_url: string;
  display_order: number;
}

const TradingServices: React.FC = () => {
  const [services, setServices] = useState<TradingService[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState('');
  const [selectedService, setSelectedService] = useState<TradingService | null>(null);
  const [isModalOpen, setIsModalOpen] = useState(false);

  useEffect(() => {
    fetchServices();
  }, []);

  const fetchServices = async () => {
    try {
      setLoading(true);
      const response = await fetch('http://localhost:8000/api/services/');
      if (response.ok) {
        const data = await response.json();
        setServices(data);
      } else {
        setError('Failed to fetch services');
      }
    } catch (err) {
      setError('Network error');
    } finally {
      setLoading(false);
    }
  };

  const handleBookService = (service: TradingService) => {
    if (service.booking_type === 'form') {
      setSelectedService(service);
      setIsModalOpen(true);
    } else {
      // Direct booking via WhatsApp, call, or email
      window.open(service.booking_url, '_blank');
    }
  };

  const handleBookingSuccess = () => {
    setIsModalOpen(false);
    setSelectedService(null);
  };

  const getBookingIcon = (bookingType: string) => {
    switch (bookingType) {
      case 'whatsapp':
        return <MessageCircle className="w-4 h-4" />;
      case 'call':
        return <PhoneCall className="w-4 h-4" />;
      case 'email':
        return <Mail className="w-4 h-4" />;
      default:
        return <MoveRight className="w-4 h-4" />;
    }
  };

  const getBookingText = (bookingType: string) => {
    switch (bookingType) {
      case 'whatsapp':
        return 'WhatsApp Now';
      case 'call':
        return 'Call Now';
      case 'email':
        return 'Email Us';
      case 'form':
        return 'Book Consultation';
      default:
        return 'Get Started';
    }
  };

  if (loading) {
    return (
      <div className="w-full py-20 lg:py-40">
        <div className="container mx-auto">
          <div className="flex text-center justify-center items-center gap-4 flex-col">
            <Badge>Trading Services</Badge>
            <div className="flex gap-2 flex-col">
              <h2 className="text-3xl md:text-5xl tracking-tighter max-w-xl text-center font-regular">
                Choose Your Trading Plan
              </h2>
              <p className="text-lg leading-relaxed tracking-tight text-muted-foreground max-w-xl text-center">
                Loading services...
              </p>
            </div>
            <div className="grid pt-20 text-left grid-cols-1 lg:grid-cols-3 w-full gap-8">
              {[1, 2, 3].map((i) => (
                <Card key={i} className="w-full rounded-md animate-pulse">
                  <CardHeader>
                    <div className="h-6 bg-gray-200 rounded mb-2"></div>
                    <div className="h-4 bg-gray-200 rounded"></div>
                  </CardHeader>
                  <CardContent>
                    <div className="h-8 bg-gray-200 rounded mb-4"></div>
                    <div className="space-y-2 mb-4">
                      <div className="h-4 bg-gray-200 rounded"></div>
                      <div className="h-4 bg-gray-200 rounded"></div>
                      <div className="h-4 bg-gray-200 rounded"></div>
                    </div>
                    <div className="h-10 bg-gray-200 rounded"></div>
                  </CardContent>
                </Card>
              ))}
            </div>
          </div>
        </div>
      </div>
    );
  }

  if (error || services.length === 0) {
    return (
      <div className="w-full py-20 lg:py-40">
        <div className="container mx-auto">
          <div className="flex text-center justify-center items-center gap-4 flex-col">
            <Badge>Trading Services</Badge>
            <div className="flex gap-2 flex-col">
              <h2 className="text-3xl md:text-5xl tracking-tighter max-w-xl text-center font-regular">
                Choose Your Trading Plan
              </h2>
              <p className="text-lg leading-relaxed tracking-tight text-muted-foreground max-w-xl text-center">
                {error || 'No services available at the moment.'}
              </p>
            </div>
          </div>
        </div>
      </div>
    );
  }

  return (
    <div className="w-full py-20 lg:py-40">
      <div className="container mx-auto">
        <div className="flex text-center justify-center items-center gap-4 flex-col">
          <Badge>Trading Services</Badge>
          <div className="flex gap-2 flex-col">
            <h2 className="text-3xl md:text-5xl tracking-tighter max-w-xl text-center font-regular">
              Choose Your Trading Plan
            </h2>
            <p className="text-lg leading-relaxed tracking-tight text-muted-foreground max-w-xl text-center">
              Professional trading services designed to maximize your market success.
            </p>
          </div>
          <div className="grid pt-20 text-left grid-cols-1 lg:grid-cols-3 w-full gap-8">
            
            {services.map((service) => (
              <Card 
                key={service.id} 
                className={`w-full rounded-md ${service.is_popular ? 'shadow-2xl border-primary' : ''}`}
              >
                <CardHeader>
                  <CardTitle>
                    <span className="flex flex-row gap-4 items-center font-normal">
                      {service.name}
                      {service.is_popular && (
                        <Badge className="ml-2">Most Popular</Badge>
                      )}
                    </span>
                  </CardTitle>
                  <CardDescription>
                    {service.description}
                  </CardDescription>
                </CardHeader>
                <CardContent>
                  <div className="flex flex-col gap-8 justify-start">
                    <p className="flex flex-row items-center gap-2 text-xl">
                      <span className="text-4xl">{service.price_display}</span>
                    </p>
                    <div className="flex flex-col gap-4 justify-start">
                      {service.features.map((feature, index) => {
                        const [title, description] = feature.includes(' - ') 
                          ? feature.split(' - ') 
                          : [feature, ''];
                        
                        return (
                          <div key={index} className="flex flex-row gap-4">
                            <Check className="w-4 h-4 mt-2 text-primary" />
                            <div className="flex flex-col">
                              <p>{title}</p>
                              {description && (
                                <p className="text-muted-foreground text-sm">
                                  {description}
                                </p>
                              )}
                            </div>
                          </div>
                        );
                      })}
                    </div>
                    <Button 
                      variant={service.is_popular ? "default" : "outline"} 
                      className="gap-4"
                      onClick={() => handleBookService(service)}
                    >
                      {getBookingText(service.booking_type)} {getBookingIcon(service.booking_type)}
                    </Button>
                  </div>
                </CardContent>
              </Card>
            ))}

          </div>
        </div>
      </div>

      {/* Service Booking Modal */}
      {selectedService && (
        <ServiceBookingModal
          service={selectedService}
          isOpen={isModalOpen}
          onClose={() => setIsModalOpen(false)}
          onSuccess={handleBookingSuccess}
        />
      )}
    </div>
  );
};

export default TradingServices;