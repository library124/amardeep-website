import { Check, MoveRight, PhoneCall } from "lucide-react";

import { Badge } from "@/components/ui/badge";
import {
  Card,
  CardContent,
  CardDescription,
  CardHeader,
  CardTitle,
} from "@/components/ui/card";
import { Button } from "@/components/ui/button";

function Pricing() {
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
            
            {/* Basic Plan */}
            <Card className="w-full rounded-md">
              <CardHeader>
                <CardTitle>
                  <span className="flex flex-row gap-4 items-center font-normal">
                    Basic Signals
                  </span>
                </CardTitle>
                <CardDescription>
                  Get started with essential trading signals and market insights
                  for consistent intraday profits.
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="flex flex-col gap-8 justify-start">
                  <p className="flex flex-row items-center gap-2 text-xl">
                    <span className="text-4xl">₹2,999</span>
                    <span className="text-sm text-muted-foreground">
                      {" "}
                      / month
                    </span>
                  </p>
                  <div className="flex flex-col gap-4 justify-start">
                    <div className="flex flex-row gap-4">
                      <Check className="w-4 h-4 mt-2 text-primary" />
                      <div className="flex flex-col">
                        <p>Daily Trading Signals</p>
                        <p className="text-muted-foreground text-sm">
                          5-7 high-probability signals daily
                        </p>
                      </div>
                    </div>
                    <div className="flex flex-row gap-4">
                      <Check className="w-4 h-4 mt-2 text-primary" />
                      <div className="flex flex-col">
                        <p>Market Analysis</p>
                        <p className="text-muted-foreground text-sm">
                          Weekly market outlook and trends
                        </p>
                      </div>
                    </div>
                    <div className="flex flex-row gap-4">
                      <Check className="w-4 h-4 mt-2 text-primary" />
                      <div className="flex flex-col">
                        <p>WhatsApp Support</p>
                        <p className="text-muted-foreground text-sm">
                          Basic support during market hours
                        </p>
                      </div>
                    </div>
                  </div>
                  <Button variant="outline" className="gap-4">
                    Start Trading <MoveRight className="w-4 h-4" />
                  </Button>
                </div>
              </CardContent>
            </Card>

            {/* Premium Plan */}
            <Card className="w-full shadow-2xl rounded-md border-primary">
              <CardHeader>
                <CardTitle>
                  <span className="flex flex-row gap-4 items-center font-normal">
                    Premium Mentorship
                    <Badge className="ml-2">Most Popular</Badge>
                  </span>
                </CardTitle>
                <CardDescription>
                  Complete trading mentorship with personalized guidance and
                  advanced strategies for serious traders.
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="flex flex-col gap-8 justify-start">
                  <p className="flex flex-row items-center gap-2 text-xl">
                    <span className="text-4xl">₹9,999</span>
                    <span className="text-sm text-muted-foreground">
                      {" "}
                      / month
                    </span>
                  </p>
                  <div className="flex flex-col gap-4 justify-start">
                    <div className="flex flex-row gap-4">
                      <Check className="w-4 h-4 mt-2 text-primary" />
                      <div className="flex flex-col">
                        <p>Premium Signals</p>
                        <p className="text-muted-foreground text-sm">
                          10-15 high-accuracy signals with detailed analysis
                        </p>
                      </div>
                    </div>
                    <div className="flex flex-row gap-4">
                      <Check className="w-4 h-4 mt-2 text-primary" />
                      <div className="flex flex-col">
                        <p>Live Trading Sessions</p>
                        <p className="text-muted-foreground text-sm">
                          Weekly live trading and strategy sessions
                        </p>
                      </div>
                    </div>
                    <div className="flex flex-row gap-4">
                      <Check className="w-4 h-4 mt-2 text-primary" />
                      <div className="flex flex-col">
                        <p>Personal Mentorship</p>
                        <p className="text-muted-foreground text-sm">
                          One-on-one guidance and portfolio review
                        </p>
                      </div>
                    </div>
                    <div className="flex flex-row gap-4">
                      <Check className="w-4 h-4 mt-2 text-primary" />
                      <div className="flex flex-col">
                        <p>Risk Management Tools</p>
                        <p className="text-muted-foreground text-sm">
                          Advanced calculators and position sizing
                        </p>
                      </div>
                    </div>
                  </div>
                  <Button className="gap-4">
                    Join Premium <MoveRight className="w-4 h-4" />
                  </Button>
                </div>
              </CardContent>
            </Card>

            {/* VIP Plan */}
            <Card className="w-full rounded-md">
              <CardHeader>
                <CardTitle>
                  <span className="flex flex-row gap-4 items-center font-normal">
                    VIP Elite
                  </span>
                </CardTitle>
                <CardDescription>
                  Exclusive access to Amardeep's personal trading strategies
                  and direct mentorship for elite traders.
                </CardDescription>
              </CardHeader>
              <CardContent>
                <div className="flex flex-col gap-8 justify-start">
                  <p className="flex flex-row items-center gap-2 text-xl">
                    <span className="text-4xl">₹24,999</span>
                    <span className="text-sm text-muted-foreground">
                      {" "}
                      / month
                    </span>
                  </p>
                  <div className="flex flex-col gap-4 justify-start">
                    <div className="flex flex-row gap-4">
                      <Check className="w-4 h-4 mt-2 text-primary" />
                      <div className="flex flex-col">
                        <p>Exclusive Strategies</p>
                        <p className="text-muted-foreground text-sm">
                          Access to Amardeep's personal trading methods
                        </p>
                      </div>
                    </div>
                    <div className="flex flex-row gap-4">
                      <Check className="w-4 h-4 mt-2 text-primary" />
                      <div className="flex flex-col">
                        <p>Direct Access</p>
                        <p className="text-muted-foreground text-sm">
                          Direct WhatsApp and call access to Amardeep
                        </p>
                      </div>
                    </div>
                    <div className="flex flex-row gap-4">
                      <Check className="w-4 h-4 mt-2 text-primary" />
                      <div className="flex flex-col">
                        <p>Portfolio Management</p>
                        <p className="text-muted-foreground text-sm">
                          Complete portfolio analysis and optimization
                        </p>
                      </div>
                    </div>
                  </div>
                  <Button variant="outline" className="gap-4">
                    Book Consultation <PhoneCall className="w-4 h-4" />
                  </Button>
                </div>
              </CardContent>
            </Card>

          </div>
        </div>
      </div>
    </div>
  );
}

export { Pricing };